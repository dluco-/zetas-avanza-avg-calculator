import { useActionData, useLoaderData, useSubmit } from "@remix-run/react";
import type { ActionFunction, LoaderFunction } from "@remix-run/server-runtime";
import Highcharts from "highcharts";
import HighchartsReact from "highcharts-react-official";
import { useEffect, useRef, useState } from "react";

interface Transaction {
  Konto?: string;
  ISIN?: string;
  ["Värdepapper/beskrivning"]?: string;
  ["Gain/loss (SEK)"]?: number;
  ["Gain/loss (%)"]?: number;
  ["Trade days"]?: number;
}

interface ApiResponse {
  period?: string;
  avg_gain?: number;
  avg_loss?: number;
  win_percentage?: number;
  total_trades?: number;
  lg_gain?: number;
  lg_loss?: number;
  avg_gain_days?: number;
  avg_loss_days?: number;
  transactions?: Transaction[];
}

export const loader: LoaderFunction = async ({ request }) => {
  const url = new URL(request.url);
  const fileName = url.searchParams.get("f");

  if (!fileName) return null;

  const response = await fetch(`http://127.0.0.1:5000/?fileName=${fileName}`);

  if (!response.ok) return null;
  return response.json();
};

export const action: ActionFunction = async ({ request }) => {
  const body = await request.formData();

  const response = await fetch("http://127.0.0.1:5000/", {
    method: "POST",
    body,
  });

  if (!response.ok) return null;

  return response.json();
};

export default function Index() {
  const submit = useSubmit();
  const loaderData = useLoaderData<ApiResponse>();
  const actionData = useActionData<ApiResponse>();

  const chartComponentRef = useRef<HighchartsReact.RefObject>(null);

  const [showRawData, setShowRawData] = useState(false);

  const [options, setOptions] = useState<Highcharts.Options>({
    chart: { type: "scatter", zoomType: "xy" },
    title: {
      text: "Gain/loss with number of trade days",
    },
    subtitle: {
      text: "A high percentage return on a few number of days is a good indicator of a good strategy.",
    },
    yAxis: {
      title: { text: "Days" },
      labels: { format: "{value}" },
    },
    xAxis: {
      title: {
        text: "Gain/loss (%)",
      },
      startOnTick: true,
      endOnTick: true,
      showLastLabel: true,
    },
    legend: { enabled: true },
    tooltip: {
      headerFormat: undefined,
      pointFormat:
        "<strong>{point.label}</strong> <br/> Percentage: {point.custom.percentage:.2f}% <br/> Amount: {point.custom.amount} SEK <br/> Days: {point.custom.days}",
    },
  });

  useEffect(() => {
    if (!loaderData && !actionData) return;

    const data = loaderData || actionData;
    const gains = data.transactions?.filter(
      (transaction) =>
        transaction["Gain/loss (%)"] && transaction["Gain/loss (%)"] > 0
    );

    const losses = data.transactions?.filter(
      (transactions) => !gains?.includes(transactions)
    );

    const setData = (data: Transaction) => ({
      label: data["Värdepapper/beskrivning"],
      y: data["Trade days"],
      x: data["Gain/loss (%)"],
      custom: {
        days: data["Trade days"],
        percentage: data["Gain/loss (%)"],
        amount: data["Gain/loss (SEK)"],
      },
    });

    setOptions({
      series: [
        {
          name: "Gain",
          type: "scatter",
          color: "green",
          data: gains?.map((t) => setData(t)),
        },
        {
          name: "Loss",
          type: "scatter",
          color: "red",
          data: losses?.map((t) => setData(t)),
        },
      ],
    });
  }, [actionData, loaderData]);

  return (
    <main className="flex flex-col p-4">
      <form
        onChange={(event) => submit(event.currentTarget)}
        method="post"
        encType="multipart/form-data"
      >
        <input
          className="w-full cursor-pointer border-4 border-red-300 bg-red-400 px-12 py-10 text-white hover:opacity-80"
          type="file"
          name="file"
        />
      </form>

      {(loaderData || actionData) && (
        <>
          <HighchartsReact
            highcharts={Highcharts}
            options={options}
            ref={chartComponentRef}
          />

          <div className="self-center">
            <button
              className="border-4 border-red-300 bg-red-400 px-4 py-3 text-white hover:opacity-80"
              onClick={() => setShowRawData(!showRawData)}
            >
              {!showRawData ? "Show JSON" : "Hide JSON"}
            </button>
          </div>
          <pre
            className={`my-4 rounded-xl bg-gray-100 p-4 ${
              !showRawData ? "hidden" : ""
            }`}
          >
            <code>{JSON.stringify(loaderData || actionData, null, 2)}</code>
          </pre>
        </>
      )}
    </main>
  );
}

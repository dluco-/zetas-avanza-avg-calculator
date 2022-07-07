import { useActionData, useLoaderData, useSubmit } from "@remix-run/react";
import type { ActionFunction, LoaderFunction } from "@remix-run/server-runtime";

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
  const loaderData = useLoaderData();
  const actionData = useActionData();

  return (
    <main className="m-4 flex flex-col">
      <form
        onChange={(event) => submit(event.currentTarget)}
        method="post"
        encType="multipart/form-data"
      >
        <input
          className="w-full cursor-pointer border-4 border-red-300 bg-red-400 px-10 py-8 text-white hover:opacity-80"
          type="file"
          name="file"
        />
      </form>

      {(loaderData || actionData) && (
        <pre className="my-4 rounded-xl bg-gray-100 p-4">
          <code>{JSON.stringify(loaderData || actionData, null, 2)}</code>
        </pre>
      )}
    </main>
  );
}

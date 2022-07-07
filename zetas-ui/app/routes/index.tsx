import { useActionData, useSubmit } from "@remix-run/react";
import type { ActionFunction } from "@remix-run/server-runtime";

export const action: ActionFunction = async ({ request }) => {
  const body = await request.formData();

  const response = await fetch("http://127.0.0.1:5000/", {
    method: "POST",
    body,
  });

  return response.json();
};

export default function Index() {
  const submit = useSubmit();
  const data = useActionData();
  return (
    <main className="m-4">
      <form
        className="my-4"
        onChange={(event) => submit(event.currentTarget)}
        method="post"
        encType="multipart/form-data"
      >
        <input
          className="px-10 py-8 cursor-pointer border-4 border-red-300 bg-red-400 text-white w-full hover:opacity-80"
          type="file"
          name="file"
        />
      </form>

      {data && (
        <pre className="m-4 rounded-xl bg-gray-100 p-4">
          <code>{JSON.stringify(data, null, 2)}</code>
        </pre>
      )}
    </main>
  );
}

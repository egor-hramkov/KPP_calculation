import { useCallback, useEffect, useMemo, useState } from "react";
import "./App.css";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { useDropzone } from "react-dropzone";
import { kppApi } from "./api/apiClient";

const apiClient = new kppApi();

function App() {
  const [code, setCode] = useState<string>();
  const decoder = useMemo(() => new TextDecoder("utf-8"),[]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles[0].arrayBuffer().then((item) => decoder.decode(new Uint8Array(item))).then((item) => setCode(item));
  }, [decoder]);

  useEffect(() => {
    apiClient.get().then((res) => console.log(res.data))
  },[])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <section className="main-wrapper">
      <div {...getRootProps()} className="dropbox">
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <p>Переместите или выберете файл JSON</p>
        )}
      </div>
      <CodeEditor
        value={code}
        language="json"
        placeholder="Вставьте код JSON."
        className="code-editor"
        onChange={(evn) => setCode(evn.target.value)}
        padding={15}
        style={{
          fontSize: 12,
          backgroundColor: "#f5f5f5",
          fontFamily:
            "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
        }}
      />
    </section>
  );
}

export default App;

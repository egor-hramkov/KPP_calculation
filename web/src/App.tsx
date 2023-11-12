import { useCallback, useEffect, useMemo, useState } from "react";
import "./App.css";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { useDropzone } from "react-dropzone";

function App() {
  const [code, setCode] = useState<string>();
  const decoder = useMemo(() => new TextDecoder("utf-8"),[]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    acceptedFiles[0].arrayBuffer().then((item) => decoder.decode(new Uint8Array(item))).then((item) => setCode(item));
  }, [decoder]);

  useEffect(() => {
    console.log(code);
  },[code])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <>
      <div {...getRootProps()}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Drop the files here ...</p>
        ) : (
          <p>Drag 'n' drop some files here, or click to select files</p>
        )}
      </div>
      <CodeEditor
        value={code}
        language="json"
        placeholder="Вставьте код JSON."
        onChange={(evn) => setCode(evn.target.value)}
        padding={15}
        style={{
          fontSize: 12,
          backgroundColor: "#f5f5f5",
          fontFamily:
            "ui-monospace,SFMono-Regular,SF Mono,Consolas,Liberation Mono,Menlo,monospace",
        }}
      />
    </>
  );
}

export default App;

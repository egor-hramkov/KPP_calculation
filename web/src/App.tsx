import { useState } from "react";
import "./App.css";
import CodeEditor from '@uiw/react-textarea-code-editor';

function App() {
  const [code, setCode] = useState<string>();

  return (
    <>
      <CodeEditor
        value={code}
        language="json"
        placeholder="Please enter JS code."
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

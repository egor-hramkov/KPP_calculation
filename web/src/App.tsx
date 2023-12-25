import { useCallback, useEffect, useState } from "react";
import "./App.scss";
import CodeEditor from "@uiw/react-textarea-code-editor";
import { kppApi } from "./api/apiClient";
import { DataList } from "./DataList/DataList";
import { TablesModal } from "./TablesView/TablesModal";
import { Aside } from "./ui/Aside";
import useAsideStore from "./store/AsideStore";
import { shallow } from "zustand/shallow";

const apiClient = new kppApi();

function App() {
  const [showModal, setShowModal] = useState<boolean>(false);
  const { setCode, setNodes } = useAsideStore((state) => state, shallow);
  const nodes = useAsideStore((state) => state.nodes, shallow);
  const code = useAsideStore((state) => state.code, shallow);

  const parser = useCallback((data: { data: object }) => {
    Object.entries(data.data).map((item, index) => {
      if (item[0] && item[1]) {
        setNodes(<DataList key={index} title={item[0]} list={item[1]} />);
      }
    });
  }, [setNodes]);

  useEffect(() => {
    apiClient.get().then((res) => {
      parser(res.data);
      setShowModal(true);
    });
  }, [parser]);

  // const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <>
      <TablesModal
        nodes={nodes}
        show={showModal}
        onExit={() => setShowModal(false)}
      />
      <section className="main-wrapper">
        <Aside />
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
    </>
  );
}

export default App;

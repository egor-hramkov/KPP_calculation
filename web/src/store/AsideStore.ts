import { ReactElement } from "react";
import { create } from "zustand";
import { devtools } from "zustand/middleware";

interface IAsideStore {
  code?: string;
  nodes: ReactElement[];
  setNodes: (node: ReactElement) => void;
  setCode: (code: string) => void;
}

const useAsideStore = create<IAsideStore>()(
  devtools(
    (set, get) => ({
      code: undefined,
      nodes: [],
      setCode: (code: string) => {
        set({ code: code }, false);
      },
      setNodes: (node: ReactElement) => {
        set({ nodes: [...get().nodes, node] }, false);
      },
    }),
    {
      name: "riasHcsStore",
    }
  )
);

export default useAsideStore;

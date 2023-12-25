import { useEffect, useState } from "react";
import "./DataList.scss";

interface Props {
  title: string;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  list: object;
  key1: number;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const transposeArray = (arr: any[][]) => {
  // Создаем новый двумерный массив
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const transposeArr: any[] = [];

  // Получаем количество столбцов и строк в исходном массиве
  const numRows = arr.length;
  const numCols = arr[0].length;

  // Перебираем столбцы и строки и заполняем новый массив
  for (let i = 0; i < numCols; i++) {
    transposeArr[i] = [];
    for (let j = 0; j < numRows; j++) {
      transposeArr[i][j] = arr[j][i];
    }
  }

  return transposeArr;
};

export const DataList = (props: Props) => {
  const [reversedArray, setReversedArray] = useState<any[]>();

  useEffect(() => {
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    const dataArray: any[] = [];
    Object.entries(props.list).map((item) => {
      dataArray.push(Object.values(item[1]));
    });
    setReversedArray(transposeArray(dataArray));
  }, [props.list]);

  return (
    <section className="data-section">
      <h1 className="data-header">{props.title}</h1>
      <table>
        <thead>
          <tr>
            {Object.entries(props.list).map((item, key) => (
              <th key={key}>{item[0]}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {reversedArray?.map((item, index) => (
            <tr key={index}>
              {item.map((item: string | number, idx: number) => {
                if (typeof item === "number") {
                  return <td key={idx}>{item.toFixed(2)}</td>;
                } else return <td key={idx}>{item}</td>;
              })}
            </tr>
          ))}
        </tbody>
      </table>
      <img src={`http://localhost:8080/static/graphics/graph_${props.key1 + 1}.png`} />
    </section>
  );
};

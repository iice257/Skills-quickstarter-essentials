import { useEffect, useState } from "react";

type GridColumns = {
  desktop: number;
  tablet: number;
  mobile: number;
};

function resolveColumns(columns: GridColumns) {
  if (window.innerWidth <= 700) return columns.mobile;
  if (window.innerWidth <= 1060) return columns.tablet;
  return columns.desktop;
}

export function useGridColumns(columns: GridColumns) {
  const [count, setCount] = useState(() => resolveColumns(columns));

  useEffect(() => {
    function handleResize() {
      setCount(resolveColumns(columns));
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [columns]);

  return count;
}

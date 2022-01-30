import { DataGrid } from "@mui/x-data-grid";
import React from "react";
import { useDispatch } from "react-redux";
import { PrepareCacheColumns } from "../../../../services/dataSourceMapperService";
import * as Style from "./style";
import { selectRow } from "./../../../../redux/slices/cacheSlice";

function CacheTable({ title, data }) {
  const columns = PrepareCacheColumns();

  const dispatch = useDispatch();

  const handleRowClick = (params) => {
    const { row } = params;

    dispatch(selectRow(row.id));
  };

  return (
    <Style.StyledTableWrapper>
      <DataGrid columns={columns} rows={data} onRowClick={handleRowClick} />
    </Style.StyledTableWrapper>
  );
}

export default CacheTable;

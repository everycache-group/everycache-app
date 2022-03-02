import { DataGrid } from "@mui/x-data-grid";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { PrepareCacheColumns } from "../../../../services/dataSourceMapperService";
import * as Style from "./style";
import { selectRow } from "./../../../../redux/slices/cacheSlice";

function CacheTable({ title, data, hideOwner }) {
  const columns = PrepareCacheColumns(hideOwner);

  const dispatch = useDispatch();
  const selectedCache = useSelector((state) => state.cache.selectedCache);

  const [selectionModel, setSelectionModel] = React.useState([]);

  const handleRowClick = (params) => {
    const { row } = params;
    setSelectionModel([row.id]);
    dispatch(selectRow(row.id));
  };

  const rowId = selectionModel[0];
  if (selectedCache && selectedCache.id != rowId) {
    setSelectionModel([selectedCache.id]);
  }

  return (
    <Style.StyledTableWrapper>
      <DataGrid columns={columns} rows={data} onRowClick={handleRowClick}
        selectionModel={selectionModel}
      />
    </Style.StyledTableWrapper>
  );
}

export default CacheTable;

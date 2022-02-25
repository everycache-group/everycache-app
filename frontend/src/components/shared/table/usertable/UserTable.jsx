import { DataGrid } from "@mui/x-data-grid";
import React from "react";
import { useDispatch, useSelector } from "react-redux";
import { PrepareUserColumns } from "../../../../services/dataSourceMapperService";
import * as Style from "./style";
import { selectRow } from "./../../../../redux/slices/userSlice";

function UserTable({ title, data }) {

  const currUserRole = useSelector((state) => state.user.role);
  const columns = PrepareUserColumns(currUserRole);

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

export default UserTable;

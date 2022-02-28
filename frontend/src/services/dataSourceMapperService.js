import localization from "./../data/localization.json";
import React from "react";
import Typography from "@mui/material/Typography";

export function createDataRow(
  cacheId,
  name,
  lon,
  lat,
  owner,
  description,
  creationDate
) {
  return {
    id: cacheId,
    name,
    description,
    owner,
    lat,
    lon,
    creationDate,
  };
}

export function PrepareCacheColumns(myCache = false) {
  const coulmns = [
    { field: "id", headerName: "ID", width: 70, hide: true, hideable: false },
    { field: "name", headerName: "Name", width: 130 },
    {
      field: "description",
      headerName: "Description",
      width: 200,
      sortable: false,

      filterable: false,
      renderCell: (params) => {
        <div>
          <Typography>{params.value}</Typography>
        </div>;
      },
    },
    {
      field: "owner",
      headerName: "Owner",
      width: 120,
      hide: myCache,
      hideable: !myCache,
    },
    { field: "lat", headerName: "Lat", width: 70, type: "number" },
    { field: "lon", headerName: "Lng", width: 70, type: "number" },
    {
      field: "creationDate",
      headerName: "Created at",
      width: 170,
      type: "date",
      valueGetter: (params) => {
        var date = new Date(params.value);
        return `${date.toLocaleString()}`;
      },
    },
  ];
  return coulmns;
}

function getVerified(columnField){
  const {value: verified} = columnField;
  return (verified) ? "Verified" : "Not Verified";
}

export function PrepareUserColumns(userRole) {
  const columns = [
    { field: "username", headerName: "Userame", width: 130 },
    { field: "role", headerName: "Role", width: 70 },
  ];

  if (userRole == "Admin") {
      columns.push({field: "email", headerName: "Email", width: 190});
      columns.push({field: "verified", headerName: "Verified", width: 110, valueGetter: getVerified});
  }
  return columns;
}

export const PrepareDataSourceTable = (cachesDto) => {
  const dataSource = [];

  cachesDto.map((cache) => {
    const {
      id,
      created_on,
      lon,
      lat,
      //TODO
      owner: { username },
      name,
      description,
    } = cache;

    dataSource.push(
      createDataRow(id, name, lon, lat, username, description, created_on)
    );
  });

  return dataSource;
};

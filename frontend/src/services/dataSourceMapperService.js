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
    lng: lon,
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
    { field: "lng", headerName: "Lng", width: 70, type: "number" },
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

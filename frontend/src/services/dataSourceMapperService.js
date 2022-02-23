import localization from "./../data/localization.json";

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

export function PrepareCacheColumns() {
  const coulmns = [
    { field: "id", headerName: "ID", width: 70, hide: true },
    { field: "name", headerName: "Name", width: 130 },
    {
      field: "description",
      headerName: "Description",
      width: 200,
      sortable: false,
      multiline: true,
      filterable: false,
    },
    { field: "owner", headerName: "Owner", width: 130 },
    { field: "lat", headerName: "Lat", width: 70, type: "number" },
    { field: "lng", headerName: "Lng", width: 70, type: "number" },
    {
      field: "creationDate",
      headerName: "Created at",
      width: 200,
      type: "date",
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

import localization from "./../data/localization.json";

function createDataRow(
  cacheId,
  name,
  lon,
  lat,
  owner,
  description,
  creationDate
) {
  return {
    cacheId,
    owner,
    name,
    lon,
    lat,
    details: [description, creationDate],
  };
}

export function PrepareDataSourceTableHeader() {
  const { owner, name, lon, lat, createdTime, description } =
    localization.cachetable;
  return {
    owner,
    name,
    lon,
    lat,
    details: [description, createdTime],
  };
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

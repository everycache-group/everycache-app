import React, { useEffect } from "react";
import { compose } from "react-recompose";
import LeafletMap from "./../../components/content/map/LeafletMap";
import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
import { useSelector, useDispatch } from "react-redux";
import withPageWrapper from "../../hoc/withPageWrapper";
import { getCaches } from "../../redux/slices/cacheSlice";
import CacheMarker from "../../components/content/cacheMarker/CacheMarker";
import CacheTable from "../../components/shared/table/cachetable/CacheTable";
import { PrepareDataSourceTableHeader } from "./../../services/dataSourceMapperService";

function Map() {
  const dispatch = useDispatch();
  const mapSettings = useSelector((state) => state.map.settings);

  useEffect(() => {
    dispatch(getCaches());
  }, []);

  const caches = useSelector((state) => state.cache.caches);

  return (
    <>
      <CacheTable data={caches} />
      <LeafletMap>
        {caches.map(({ id, lat, lng, description }) => {
          return (
            <CacheMarker key={id} position={[lat, lng]} title={description} />
          );
        })}
        <SettingsMapTracker
          zoom={mapSettings.zoom}
          center={mapSettings.center}
        />
      </LeafletMap>
    </>
  );
}

export default compose(withPageWrapper)(Map);

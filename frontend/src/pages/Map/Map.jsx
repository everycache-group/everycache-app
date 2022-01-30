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

  const tableHeader = PrepareDataSourceTableHeader();

  return (
    <>
      <CacheTable title="Caches" header={tableHeader} data={caches} />
      <LeafletMap>
        {caches.map((cache) => {
          return (
            <CacheMarker
              key={cache.cacheId}
              position={[cache.lat, cache.lon]}
              title={cache.description}
            />
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

import React, { useEffect } from "react";
import { compose } from "react-recompose";
import LeafletMap from "./../../components/content/map/LeafletMap";
import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
import { useSelector, useDispatch } from "react-redux";
import withPageWrapper from "../../hoc/withPageWrapper";
import { getCaches } from "../../redux/slices/cacheSlice";
import CacheMarker from "../../components/content/cacheMarker/CacheMarker";
import CacheTable from "../../components/shared/table/cachetable/CacheTable";
import * as Style from "./style";
import CacheMenu from "../../components/navigation/CacheMenu/CacheMenu";
import { Typography } from "@mui/material";

function Map() {
  const dispatch = useDispatch();
  const mapSettings = useSelector((state) => state.map.settings);

  useEffect(() => {
    dispatch(getCaches());
  }, []);

  const caches = useSelector((state) => state.cache.caches);

  return (
    <>
      <Style.CacheContent>
        <Typography variant="h4">All Caches</Typography>
        <br />
        <CacheTable data={caches} hideOwner={false} />
      </Style.CacheContent>

      <LeafletMap width={1200}>
        {caches.map(({ id, lat, lon, description }) => {
          return (
            <CacheMarker key={id} position={[lat, lon]} title={description} />
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

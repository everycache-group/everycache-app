import React, { useEffect } from "react";
import { compose } from "react-recompose";
import LeafletMap from "./../../components/content/map/LeafletMap";
import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
import { useSelector, useDispatch } from "react-redux";
import withPageWrapper from "../../hoc/withPageWrapper";
import { getMyCaches } from "../../redux/slices/cacheSlice";
import CacheMarker from "../../components/content/cacheMarker/CacheMarker";
import CacheTable from "../../components/shared/table/cachetable/CacheTable";
import * as Style from "./style";
import CacheMenu from "../../components/navigation/CacheMenu/CacheMenu";
import { Typography } from "@mui/material";

function MyMap() {
  const dispatch = useDispatch();
  const mapSettings = useSelector((state) => state.map.settings);

  useEffect(() => {
    dispatch(getMyCaches());
  }, []);

  const caches = useSelector((state) => state.cache.caches);

  return (
    <>
      <Style.CacheContent>
        <Typography variant="h4">My Caches</Typography>
        <br />
        <CacheMenu />
        <CacheTable data={caches} hideOwner={true} />
      </Style.CacheContent>

      <LeafletMap width={1200}>
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

export default compose(withPageWrapper)(MyMap);

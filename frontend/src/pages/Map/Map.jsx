import React from "react";
import { compose } from "react-recompose";
import CacheCreator from "../../components/content/caches/cacheCreator/CacheCreator";
import LeafletMap from "./../../components/content/map/LeafletMap";
import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
import { useSelector } from "react-redux";
import withPageWrapper from "../../hoc/withPageWrapper";

function Map() {
  const mapSettings = useSelector((state) => state.map.settings);

  return (
    <>
      <CacheCreator />
      <LeafletMap>
        <SettingsMapTracker
          zoom={mapSettings.zoom}
          center={mapSettings.center}
        />
      </LeafletMap>
    </>
  );
}

export default compose(withPageWrapper)(Map);

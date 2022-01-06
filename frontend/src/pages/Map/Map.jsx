import React from "react";
import PageWrapper from "../../components/common/wrappers/PageWrapper";
import CacheCreator from "../../components/content/caches/cacheCreator/CacheCreator";
import LeafletMap from "./../../components/content/map/LeafletMap";
import SettingsMapTracker from "../../components/content/map/SettingsMapTracker";
import { useSelector } from "react-redux";

function Map() {
  const mapSettings = useSelector((state) => state.map.settings);

  return (
    <PageWrapper>
      <CacheCreator />
      <LeafletMap>
        <SettingsMapTracker
          zoom={mapSettings.zoom}
          center={mapSettings.center}
        />
      </LeafletMap>
    </PageWrapper>
  );
}

export default Map;

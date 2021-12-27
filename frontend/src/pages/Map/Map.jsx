import React from "react";
import PageWrapper from "../../components/common/wrappers/PageWrapper";
import CacheCreator from "../../components/content/caches/cacheCreator/CacheCreator";
import LeafletMap from "./../../components/content/map/LeafletMap";

function Map() {
  return (
    <PageWrapper>
      <CacheCreator />
      <LeafletMap />
    </PageWrapper>
  );
}

export default Map;

import React from "react";
import { compose } from "react-recompose";
import withPageWrapper from "../../hoc/withPageWrapper";
import DeleteCachePopup from "./../../components/content/CachePopup/DeleteCachePopup/DeleteCachePopup";

const Home = () => {
  return (
    <>
      <p>Home Page Construction</p>
    </>
  );
};

export default compose(withPageWrapper)(Home);

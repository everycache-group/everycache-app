import React from "react";
import { compose } from "react-recompose";
import RatingCommentCache from "../../components/content/Rating/RatingCommentCache";
import withPageWrapper from "../../hoc/withPageWrapper";
import DeleteCachePopup from "./../../components/content/CachePopup/DeleteCachePopup/DeleteCachePopup";

const Home = () => {
  return (
    <>
      <RatingCommentCache />
      <p>Home Page Construction</p>
    </>
  );
};

export default compose(withPageWrapper)(Home);

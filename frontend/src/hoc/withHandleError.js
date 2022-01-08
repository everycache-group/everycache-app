import React from "react";
import Error from "../components/shared/interaction/error/Error";

const withHandleError =
  (Component) =>
  ({ error, ...props }) => {
    if (error) {
      return <Error message={error} />;
    }
    return <Component {...props} />;
  };

export default withHandleError;

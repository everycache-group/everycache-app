import CircularProgress from "@mui/material/CircularProgress";
import React from "react";

const withLoading =
  (Component) =>
  ({ loading, ...props }) => {
    if (loading) {
      return <CircularProgress />;
    }
    return <Component {...props} />;
  };

export default withLoading;

import { CircularProgress } from "@mui/material";
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

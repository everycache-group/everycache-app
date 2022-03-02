import React from "react";
import { compose } from "react-recompose";
import withPageWrapper from "../../hoc/withPageWrapper";

function NotFound() {
  return <div>404 - page not Found :(</div>;
}

export default compose(withPageWrapper)(NotFound);

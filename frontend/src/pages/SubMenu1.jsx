import React from "react";
import PageWrapper from "../components/common/wrappers/PageWrapper";
import { useSelector } from "react-redux";

const SubMenu1 = () => {
  const username = useSelector((state) => state.user.username);

  return (
    <PageWrapper>
      <h1>Welcome {username}!</h1>
    </PageWrapper>
  );
};

export default SubMenu1;

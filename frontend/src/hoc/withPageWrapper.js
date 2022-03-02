import React from "react";
import styled from "styled-components";
import { useSelector } from "react-redux";

export const PageWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 100vh;
  width: 100%;
  transition: padding-left 300ms ease-in-out;
  padding: 15px;
  padding-top: 93px;
  padding-left: ${({ sidebar }) => (sidebar ? "265px" : "0")};
`;

const withPageWrapper =
  (Component) =>
  ({ ...props }) => {
    const sidebarVisible = useSelector(
      (state) => state.navigation.sidebarVisible
    );
    return (
      <PageWrapper sidebar={sidebarVisible}>
        <Component {...props} />
      </PageWrapper>
    );
  };

export default withPageWrapper;

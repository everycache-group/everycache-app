import React from "react";
import styled from "styled-components";
import { useSelector } from "react-redux";

export const PageWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
  flex-wrap: wrap;
  height: 90vh;
  margin-left: ${({ sidebar }) => (sidebar ? "250px" : "0")};
  transition: margin-left 300ms ease-in-out;
  padding: 15px;
  padding-top: 93px;
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

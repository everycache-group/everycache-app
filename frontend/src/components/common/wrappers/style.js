import styled from "styled-components";

export const PageWrapper = styled.div`
  display: flex;
  align-items: center;
  justify-content: space-around;
  height: 90vh;
  margin-left: ${({ sidebar }) => (sidebar ? "250px" : "0")};
  transition: margin-left 300ms ease-in-out;
  padding: 15px;
  padding-top: 93px;
`;

import styled from "styled-components";
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';


export const UserFormWrapper = styled.div`
  border: 1px solid #ccc;
  height: 350px;
  padding: 16px;
  border-radius: 25px;
  display: grid;
  justify-content: center;
  align-items: center;
`;

export const UserTextField = styled(TextField)`
  && {
  }
`;

export const UserFormControl = styled(FormControl)`
  && {
    margin: 5px 3px;
    width: 150px;
  }
`;

export const SelectWrapper = styled.div`
  display: flex;
  justify-content: space-between;
`

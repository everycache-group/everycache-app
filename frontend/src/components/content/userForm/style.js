import styled from "styled-components";
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';


export const UserFormWrapper = styled.form`
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 25px;
  display: grid;
  justify-content: center;
  align-items: center;
`;

export const UserTextField = styled(TextField)`
  && {
    margin: 10px 0;
  }
`;

export const UserFormControl = styled(FormControl)`
  && {
    margin: 5px 3px;
    width: 130px;
  }
`;

export const SelectWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
`

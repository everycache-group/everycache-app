import styled from "styled-components";
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';


export const CommentFormWrapper = styled.form`
  border: 1px solid #ccc;
  padding: 16px;
  border-radius: 25px;
  display: grid;
  justify-content: center;
  align-items: center;
`;

export const CommentTextField = styled(TextField)`
  && {
    margin: 10px 0;
  }
`;

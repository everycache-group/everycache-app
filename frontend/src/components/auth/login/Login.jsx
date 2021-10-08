import React, {useState} from 'react'
import * as Style from './style'
import TextField from '@mui/material/TextField'
import LoadingButton from '@mui/lab/LoadingButton'
import useForm from '../../../hooks/useForm'
import * as auth from '../../../services/authService'




function Login() {
    const [registering, setRegistering]= useState(false);

    const {handleFormSubmit, handleUserInput, formValues, errors} = useForm({
        email: "",  password: "",}
        , () => {
        const {email, password} = formValues;
        
        auth.loginUser(email, password).then(response => {
            
        }).catch(x => "Login Failed");
    });


    return (
        <Style.LoginForm>
                <TextField size="small" id="username"  error={!!errors.username} helperText={errors.username} onChange={handleUserInput}  type="username" name="username" label="Username"/>
                <TextField size="small" id="email"     error={!!errors.email} helperText={errors.email} onChange={handleUserInput}  type="email"    name="email"    label="Email"/>
                <TextField size="small" id="password"  error={!!errors.password} helperText={errors.password} onChange={handleUserInput}  type="password" name="password" label="Password"/>
               
                <LoadingButton 
                 onClick={handleFormSubmit}
                 loading={registering}
                 variant="contained"
                 color="success"
                 >
                    Log in
                </LoadingButton>
        </Style.LoginForm>
    )
}

export default Login

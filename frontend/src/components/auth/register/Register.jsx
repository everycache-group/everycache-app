import React, {useState} from 'react'
import * as Style from './style'
import TextField from '@mui/material/TextField'
import LoadingButton from '@mui/lab/LoadingButton'
import {Redirect} from 'react-router-dom'
import * as user from './../../../services/userService';

import  useForm  from '../../../hooks/useForm';



function Register() {
    const [registering, setRegistering]= useState(false);

    const {handleFormSubmit, handleUserInput, formValues, errors} = useForm({
        username: "",
        email: "",
        password: "",
        password2: ""
    }, () => {
        const {username, email, password} = formValues;
        user.create(username, email, password).then(() => "XD");
    });
    
    return (
        <div>
            <Style.RegisterForm>
                <TextField size="small" id="username"  error={!!errors.username} helperText={errors.username} onChange={handleUserInput}  type="username" name="username" label="Username"/>
                <TextField size="small" id="email"     error={!!errors.email} helperText={errors.email} onChange={handleUserInput}  type="email"    name="email"    label="Email"/>
                <TextField size="small" id="password"  error={!!errors.password} helperText={errors.password} onChange={handleUserInput}  type="password" name="password" label="Password"/>
                <TextField size="small" id="password2" error={!!errors.password2} helperText={errors.password2} onChange={handleUserInput}  type="password" name="password2" label="Repeat Password"/>
                
                <LoadingButton 
                 onClick={handleFormSubmit}
                 loading={registering}
                 variant="contained"
                 color="success"
                 >
                    Register
                </LoadingButton>
            </Style.RegisterForm>
        </div>
    )
}

export default Register
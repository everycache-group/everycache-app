const validate = (values) => {
    let errors = {};

    if(!values.username)
        errors.username ="Username is required."
    
        
    if(!values.email)
        errors.email = "Email is required."
    else if(!/\S+@\S+\.\S+/.test(values.email))
        errors.email = "Email is invalid."


    if(!values.password)
        errors.password="Password is required."


    if(!values.password2)
        errors.password2="Password is required."
    else if(values.password !== values.password2)
        errors.password2="Both passwords must be equal."

    return errors;
}

export default validate;


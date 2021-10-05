import { useState, useEffect, useRef} from 'react'
import validation from './../services/validationFormService'

const useForm = (initialFormValues, formValidHandler) => {
    const [formValues, setFormValues] = useState(initialFormValues);
    const [errors, setErrors] = useState({});
    const [formValid, setFormValid]= useState(false);
    const isInitialMount = useRef(true);
  

    const handleUserInput = e => {
        const name = e.target.name;
        const value = e.target.value;
        
        setFormValues({...formValues,
                      [name]: value});
    }

    const handleFormSubmit = e => {
        e.preventDefault();
        setErrors(validation(formValues));
        
    };

    useEffect(() => {
        if(isInitialMount.current)
        {
            isInitialMount.current = false;
        } else {
            const formOk = Object.keys(errors).length === 0; // if no errors
            if(formOk && formValidHandler instanceof Function)
            formValidHandler();
        }
    }, [errors])

    return {handleFormSubmit, handleUserInput,  errors, formValues, formValid};
}

export default useForm;
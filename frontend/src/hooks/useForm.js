import { useState, useEffect, useRef } from "react";

const useForm = (initialFormValues, callback) => {
  const [formValues, setFormValues] = useState(initialFormValues);
  const [errors, setErrors] = useState({});
  const [formValid, setFormValid] = useState(false);
  const isInitialMount = useRef(true);

  const handleUserInput = (e) => {
    const name = e.target.name;
    let value = e.target.value;

    if (e.target.type === "number") {
      value = parseFloat(e.target.value);
    }

    setFormValues({ ...formValues, [name]: value });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    callback();
  };

  return {
    handleFormSubmit,
    handleUserInput,
    errors,
    formValues,
    formValid,
    setFormValues,
    setErrors
  };
};

export default useForm;

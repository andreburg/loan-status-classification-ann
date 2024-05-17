// src/LoanForm.js
import React, { useContext, useState } from 'react';
import { TextField, Button, Typography, Grid, FormControl, InputLabel, Select, MenuItem, Slider, Box, FormControlLabel, Switch, RadioGroup, Radio } from '@mui/material';
import 'react-toastify/dist/ReactToastify.css';
import { useToasts } from 'react-toast-notifications';
import { loanApplicationsContext } from '../../lib/Context';

const LoanForm = ({ onClose }) => {
    const [formData, setFormData] = useState({
        gender: '',
        married: '',
        dependents: '',
        education: '',
        self_employed: '',
        applicant_income: 5000,
        coapplicant_income: 2000,
        loan_amount: 300000,
        loan_amount_term: 360,
        property_area: '',
        credit_history: ''
    });

    const [formErrors, setFormErrors] = useState({});
    const [loanApplications, setLoanApplications] = useContext(loanApplicationsContext);
    const { addToast } = useToasts();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
        setFormErrors({ ...formErrors, [name]: '' });
    };

    const handleSliderChange = (name) => (event, newValue) => {
        setFormData({ ...formData, [name]: newValue });
    };

    const validateForm = () => {
        const errors = {};
        // Check for required fields
        if (!formData.gender) errors.gender = 'Gender is required';
        if (!formData.married) errors.married = 'Marital status is required';
        if (!formData.dependents) errors.dependents = 'Dependents count is required';
        if (!formData.education) errors.education = 'Education status is required';
        if (!formData.self_employed) errors.self_employed = 'Self-employed status is required';
        if (!formData.property_area) errors.property_area = 'Property area is required';
        if (!formData.credit_history) errors.credit_history = 'Credit history is required';

        setFormErrors(errors);
        return Object.keys(errors).length === 0; // Form is valid if there are no errors
    };

    const handleLoanPrediction = async () => {
        const isFormValid = validateForm();

        if (isFormValid) {
            try {
                const response = await fetch('https://bc-loan-application-server.onrender.com/predict', {
                    method: 'POST',
                    mode: 'cors',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData),
                });

                if (!response.ok) {
                    throw new Error('Failed to predict loan status');
                }

                const data = await response.json();
                if (data) {
                    setLoanApplications([...loanApplications, data[0]])
                    if (data[0]['loan_status'] == 'Approved') {
                        addToast('Loan Application Approved', { appearance: 'success' });
                    } else {
                        addToast('Loan Application Rejected', { appearance: 'error' });
                    }

                    setTimeout(() => {
                        onClose();
                    }, 2000);
                    onClose();
                }
            } catch (error) {
                console.error('Error predicting loan status:', error);
            }
        }
    };

    return (
        <div>
            <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="gender">Gender</InputLabel>
                        <Select
                            value={formData.gender}
                            onChange={handleChange}
                            label="Gender"
                            inputProps={{
                                name: 'gender',
                                id: 'gender',
                            }}
                            error={formErrors.gender}
                        >
                            <MenuItem value="Male">Male</MenuItem>
                            <MenuItem value="Female">Female</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="married">Married</InputLabel>
                        <Select
                            value={formData.married}
                            onChange={handleChange}
                            label="Married"
                            inputProps={{
                                name: 'married',
                                id: 'married',
                            }}
                            error={formErrors.married}
                        >
                            <MenuItem value="Yes">Yes</MenuItem>
                            <MenuItem value="No">No</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="dependents">Dependents</InputLabel>
                        <Select
                            value={formData.dependents}
                            onChange={handleChange}
                            label="Dependents"
                            inputProps={{
                                name: 'dependents',
                                id: 'dependents',
                            }}
                            error={!!formErrors.dependents}
                        >
                            <MenuItem value="0">0</MenuItem>
                            <MenuItem value="1">1</MenuItem>
                            <MenuItem value="2">2</MenuItem>
                            <MenuItem value="3+">3+</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="education">Education</InputLabel>
                        <Select
                            value={formData.education}
                            onChange={handleChange}
                            label="Education"
                            inputProps={{
                                name: 'education',
                                id: 'education',
                            }}
                            error={formErrors.education}
                        >
                            <MenuItem value="Graduate">Graduate</MenuItem>
                            <MenuItem value="Not Graduate">Not Graduate</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="propertyArea">Property Area</InputLabel>
                        <Select
                            value={formData.property_area}
                            onChange={handleChange}
                            label="Property Area"
                            inputProps={{
                                name: 'property_area',
                                id: 'property_area',
                            }}
                            error={formErrors.property_area}
                        >
                            <MenuItem value="Rural">Rural</MenuItem>
                            <MenuItem value="Semiurban">Semiurban</MenuItem>
                            <MenuItem value="Urban">Urban</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="self_employed">Self Employed</InputLabel>
                        <Select
                            value={formData.self_employed}
                            onChange={handleChange}
                            label="Self Employed"
                            inputProps={{
                                name: 'self_employed',
                                id: 'self_employed',
                            }}
                            error={formErrors.self_employed}
                        >
                            <MenuItem value="Yes">Yes</MenuItem>
                            <MenuItem value="No">No</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12} sm={6}>
                    <FormControl fullWidth variant="outlined">
                        <InputLabel htmlFor="credit_history">Credit History</InputLabel>
                        <Select
                            value={formData.credit_history}
                            onChange={handleChange}
                            label="Credit History"
                            inputProps={{
                                name: 'credit_history',
                                id: 'credit_history',
                            }}
                            error={formErrors.credit_history}
                        >
                            <MenuItem value={"1"}>Yes</MenuItem>
                            <MenuItem value={"0"}>No</MenuItem>
                        </Select>
                    </FormControl>
                </Grid>
                <Grid item xs={12}>
                    <Typography id="applicantIncomeSliderLabel">Applicant Income: {formData.applicant_income}</Typography>
                    <Slider
                        aria-labelledby="applicantIncomeSliderLabel"
                        value={formData.applicant_income}
                        min={0}
                        max={100000}
                        step={500}
                        onChange={handleSliderChange('applicant_income')}
                        valueLabelDisplay="auto"
                    />
                </Grid>
                <Grid item xs={12}>
                    <Typography id="coapplicantIncomeSliderLabel">Co-applicant Income: {formData.coapplicant_income}</Typography>
                    <Slider
                        aria-labelledby="coapplicantIncomeSliderLabel"
                        value={formData.coapplicant_income}
                        min={0}
                        max={100000}
                        step={500}
                        onChange={handleSliderChange('coapplicant_income')}
                        valueLabelDisplay="auto"
                    />
                </Grid>
                <Grid item xs={12}>
                    <Typography id="loanAmountSliderLabel">Loan Amount: {formData.loan_amount}</Typography>
                    <Slider
                        aria-labelledby="loanAmountSliderLabel"
                        value={formData.loan_amount}
                        min={100}
                        max={100000}
                        step={100}
                        onChange={handleSliderChange('loan_amount')}
                        valueLabelDisplay="auto"
                    />
                </Grid>
                <Grid item xs={12}>
                    <Typography id="loanAmountTermSliderLabel">Loan Amount Term (months): {formData.loan_amount_term}</Typography>
                    <Slider
                        aria-labelledby="loanAmountTermSliderLabel"
                        value={formData.loan_amount_term}
                        min={12}
                        max={720}
                        step={12}
                        onChange={handleSliderChange('loan_amount_term')}
                        valueLabelDisplay="auto"
                    />
                </Grid>
            </Grid>
            <Button variant="contained" color="primary" onClick={handleLoanPrediction}>
                Submit
            </Button>
        </div>
    );
};

export default LoanForm;


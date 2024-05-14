import React, { useEffect, useState } from 'react';
import {
    Typography,
    AppBar,
    Toolbar,
    Button,
    Container,
    IconButton,
    Box,
    Modal,
    Paper,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
} from '@mui/material';
import { Add } from '@mui/icons-material';
import { makeStyles } from '@mui/styles';
import LoanForm from '../LoanForm/LoanForm';
import './index.css'
import LoanTable from '../LoanTable/LoanTable';

const useStyles = makeStyles((theme) => ({
    appBar: {
        width: '100%',
        backgroundColor: 'rgb(24, 24, 24)',
    },
    addButton: {
        borderRadius: '50%',
        width: theme.spacing(8),
        height: theme.spacing(8),
        backgroundColor: theme.palette.primary.main,
        color: theme.palette.common.white,
        '&:hover': {
            backgroundColor: theme.palette.primary.dark,
        },
    },
    addButtonContainer: {
        position: 'fixed',
        top: theme.spacing(13),
        right: theme.spacing(3),
        zIndex: 999,
    },
}));

const Dashboard = () => {
    const [isFormOpen, setIsFormOpen] = useState(false);
    const [page, setPage] = useState(0);
    const [rowsPerPage, setRowsPerPage] = useState(5);
    const classes = useStyles();
    const attributes = ['loan_id', 'gender', 'married', 'dependents', 'education', 'self_employed', 'applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term', 'credit_history', 'property_area', 'loan_status']

    const handleOpenForm = () => {
        setIsFormOpen(true);
    };

    const handleCloseForm = () => {
        setIsFormOpen(false);
    };

    return (
        <div>
            <div className='dashboard-table-container'>
                <Box className={classes.addButtonContainer}>
                    <IconButton className={classes.addButton} onClick={handleOpenForm}>
                        <Add fontSize="large" />
                    </IconButton>
                </Box>

                <Paper sx={{ width: '100%', overflowX: 'auto', marginTop: 4 }}>
                    <LoanTable />
                </Paper>

                <Modal
                    open={isFormOpen}
                    onClose={handleCloseForm}
                    aria-labelledby="loan-form-modal"
                    aria-describedby="loan-form-modal-description"
                >
                    <Box
                        sx={{
                            position: 'absolute',
                            top: '50%',
                            left: '50%',
                            transform: 'translate(-50%, -50%)',
                            bgcolor: 'background.paper',
                            boxShadow: 24,
                            p: 4,
                            minWidth: 400,
                            maxWidth: '80%',
                            borderRadius: 2,
                        }}
                    >
                        <Typography variant="h5" gutterBottom>
                            Create New Loan Application
                        </Typography>
                        <LoanForm onClose={handleCloseForm} />
                    </Box>
                </Modal>
            </div>
        </div>
    );
};

export default Dashboard;

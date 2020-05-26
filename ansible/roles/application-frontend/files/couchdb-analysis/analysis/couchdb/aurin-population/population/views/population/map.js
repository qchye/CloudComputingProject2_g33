function (doc) {
    emit(doc.gcc_name16, 
    {med_year: doc.med_years, working_age_pop_pr100: doc.working_age_pop_pr100, 
     elderly_pop_pr100: Math.round((100-doc.working_age_pop_pr100-doc.young_pop_pr100)*10) / 10});
}
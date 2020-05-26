function (doc) {
    var state_code = String(doc.sa2_main11).charAt(0);
    var state;
    if (state_code == '1') {
      state = 'NSW'
    }
    else if (state_code == '2') {
      state = 'VIC'
    }
    else if (state_code == '3') {
      state = 'QLD'
    }
    else if (state_code == '4') {
      state = 'SA'
    }
    else if (state_code == '5') {
      state = 'WA'
    }
    else if (state_code == '6') {
      state = 'TAS'
    }
    else if (state_code == '7') {
      state = 'NT'
    }
    else if (state_code == '8') {
      state = 'ACT'
    }
    else {
      state = 'OT'
    }
    emit(state, [doc.dec_2010, doc.dec_2011, doc.dec_2012, doc.dec_2013, doc.dec_2014, doc.dec_2015, doc.dec_2016, doc.dec_2017]);
  }
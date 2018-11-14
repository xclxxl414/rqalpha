# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from rqalpha.const import COMMISSION_TYPE, MARGIN_TYPE


CN_FUTURE_INFO = {
    "SM": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "SR": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "JD": {
        "hedge": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.00015,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.00015,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 0.00015
=======
            "open_commission_ratio": 0.00015,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.00015,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.00015,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 0.00015
=======
            "open_commission_ratio": 0.00015,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.00015,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.00015,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 0.00015
=======
            "open_commission_ratio": 0.00015,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "T": {
        "hedge": {
            "short_margin_ratio": 0.02,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.02,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.02,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.02,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.02,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.02,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        }
    },
    "P": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "BB": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        }
    },
    "RM": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "RS": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "J": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        }
    },
    "RI": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "ER": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2.5,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "L": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "PP": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "SN": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        }
    },
    "I": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        }
    },
    "TA": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "AL": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "ZC": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        }
    },
    "TC": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4.0
=======
            "open_commission_ratio": 4.0,
            "tick_size": 0.2,
>>>>>>> upstream/master
        }
    },
    "LR": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "RU": {
        "hedge": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 4.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 4.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 4.5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "M": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "TF": {
        "hedge": {
            "short_margin_ratio": 0.012,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.012,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.012,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.012,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.012,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.012,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 0.005,
>>>>>>> upstream/master
        }
    },
    "MA": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "ME": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.4,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.4
=======
            "open_commission_ratio": 1.4,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "WR": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 4e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 4e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 4e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "RB": {
        "hedge": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4.5e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4.5e-05
=======
            "open_commission_ratio": 4.5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "C": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.2,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.2
=======
            "open_commission_ratio": 1.2,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.2,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.2
=======
            "open_commission_ratio": 1.2,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.2,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.2
=======
            "open_commission_ratio": 1.2,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "JR": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 3.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "SF": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "OI": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "RO": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "CF": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.3,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.3
=======
            "open_commission_ratio": 4.3,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.3,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4.3
=======
            "open_commission_ratio": 4.3,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.3,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4.3
=======
            "open_commission_ratio": 4.3,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "BU": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 3e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 3e-05
=======
            "open_commission_ratio": 3e-05,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 3e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 3e-05
=======
            "open_commission_ratio": 3e-05,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 3e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3e-05
=======
            "open_commission_ratio": 3e-05,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "JM": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 3e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 6e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 6e-05
=======
            "open_commission_ratio": 6e-05,
            "tick_size": 0.5,
>>>>>>> upstream/master
        }
    },
    "IH": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.4,
            "close_commission_today_ratio": 0.0023,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.3e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.4,
<<<<<<< HEAD
            "open_commission_ratio": 2.3e-05
=======
            "open_commission_ratio": 2.3e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        }
    },
    "FG": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "PM": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 5.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 5.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 5.0
=======
            "open_commission_ratio": 5.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 5.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 5.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 5.0
=======
            "open_commission_ratio": 5.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 5.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 5.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 5.0
=======
            "open_commission_ratio": 5.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "FB": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 5e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 0.0001,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 0.0001
=======
            "open_commission_ratio": 0.0001,
            "tick_size": 0.05,
>>>>>>> upstream/master
        }
    },
    "CS": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 1.5
=======
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "B": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "IC": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.4,
            "close_commission_today_ratio": 0.0023,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.3e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.4,
<<<<<<< HEAD
            "open_commission_ratio": 2.3e-05
=======
            "open_commission_ratio": 2.3e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        }
    },
    "WH": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "WS": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "FU": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 2e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2e-05
=======
            "open_commission_ratio": 2e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 2e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2e-05
=======
            "open_commission_ratio": 2e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 2e-05,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2e-05
=======
            "open_commission_ratio": 2e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "AU": {
        "hedge": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 10.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 10.0
=======
            "open_commission_ratio": 10.0,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 10.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 10.0
=======
            "open_commission_ratio": 10.0,
            "tick_size": 0.05,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 10.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 10.0
=======
            "open_commission_ratio": 10.0,
            "tick_size": 0.05,
>>>>>>> upstream/master
        }
    },
    "CU": {
        "hedge": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 10.0,
>>>>>>> upstream/master
        }
    },
    "V": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "Y": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.5,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.5
=======
            "open_commission_ratio": 2.5,
            "tick_size": 2.0,
>>>>>>> upstream/master
        }
    },
    "AG": {
        "hedge": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.08,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.08,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 5e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 5e-05
=======
            "open_commission_ratio": 5e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "PB": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 5.0,
>>>>>>> upstream/master
        }
    },
    "IF": {
        "hedge": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.4,
            "close_commission_today_ratio": 0.0023,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.3e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.4,
<<<<<<< HEAD
            "open_commission_ratio": 2.3e-05
=======
            "open_commission_ratio": 2.3e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.2,
            "close_commission_today_ratio": 0.000115,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 2.5e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.2,
<<<<<<< HEAD
            "open_commission_ratio": 2.5e-05
=======
            "open_commission_ratio": 2.5e-05,
            "tick_size": 0.2,
>>>>>>> upstream/master
        }
    },
    "A": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 2.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 2.0
=======
            "open_commission_ratio": 2.0,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "NI": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 6.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 6.0
=======
            "open_commission_ratio": 6.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 6.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
<<<<<<< HEAD
            "open_commission_ratio": 6.0
=======
            "open_commission_ratio": 6.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 6.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 6.0
=======
            "open_commission_ratio": 6.0,
            "tick_size": 10.0,
>>>>>>> upstream/master
        }
    },
    "HC": {
        "hedge": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_MONEY,
            "close_commission_ratio": 4e-05,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 4e-05
=======
            "open_commission_ratio": 4e-05,
            "tick_size": 1.0,
>>>>>>> upstream/master
        }
    },
    "ZN": {
        "hedge": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "speculation": {
            "short_margin_ratio": 0.06,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.06,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
>>>>>>> upstream/master
        },
        "arbitrage": {
            "short_margin_ratio": 0.0,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": None,
            "long_margin_ratio": 0.0,
<<<<<<< HEAD
            "open_commission_ratio": 3.0
        }
=======
            "open_commission_ratio": 3.0,
            "tick_size": 5.0,
        }
    },
    "CY": {
        "hedge": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
            "open_commission_ratio": 4.0,
            "tick_size": 5.0,
        },
        "speculation": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
            "open_commission_ratio": 4.0,
            "tick_size": 5.0,
        },
        "arbitrage": {
            "short_margin_ratio": 0.05,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 4.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.05,
            "open_commission_ratio": 4.0,
            "tick_size": 5.0,
        }
    },
    "AP": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
        },
        "arbitrage": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 1.5,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 1.5,
            "tick_size": 1.0,
        }
    },
    "SC": {
        "hedge": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 20.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 20.0,
            "tick_size": 0.1,
        },
        "speculation": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 20.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 20.0,
            "tick_size": 0.1,
        },
        "arbitrage": {
            "short_margin_ratio": 0.07,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 20.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.07,
            "open_commission_ratio": 20.0,
            "tick_size": 0.1,
        }
    },
    "TS": {
        "hedge": {
            "short_margin_ratio": 0.005,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.005,
            "open_commission_ratio": 3,
            "tick_size": 0.005,
        },
        "speculation": {
            "short_margin_ratio": 0.005,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.005,
            "open_commission_ratio": 3,
            "tick_size": 0.005,
        },
        "arbitrage": {
            "short_margin_ratio": 0.005,
            "close_commission_today_ratio": 0.0,
            "commission_type": COMMISSION_TYPE.BY_VOLUME,
            "close_commission_ratio": 3.0,
            "margin_type": MARGIN_TYPE.BY_MONEY,
            "long_margin_ratio": 0.005,
            "open_commission_ratio": 3,
            "tick_size": 0.005,
        },
>>>>>>> upstream/master
    }
}


pub struct Trial;

use log::{debug, error, info, trace, warn};

impl Trial {
    pub fn new() -> Self {
        debug!("Debug in new()");
        error!("Error in new()");
        Self
    }

    pub fn add(&self, num1: i32, num2: i32) -> i32 {
        let sum1 = num1 + num2;
        info!("Num1: {}", num1);
        trace!("Num2: {}", num2);
        warn!("Sum: {}", sum1);
        sum1
    }
}

#!/usr/bin/env python3
"""
Test script to reproduce the issue described in the problem statement.
"""
import xarray as xr
import numpy as np


class HasValues(object):
    """Object with a values property to test the issue."""
    values = 5


def test_issue_reproduction():
    """Test that reproduces the original issue."""
    print("Testing the issue with Variable.__setitem__ coercing types...")
    
    good_indexed, bad_indexed = xr.DataArray([None]), xr.DataArray([None])
    
    # This should work fine
    good_indexed.loc[{'dim_0': 0}] = set()
    print(f"good_indexed.values: {good_indexed.values}")
    print(f"Type of first element in good_indexed: {type(good_indexed.values[0])}")
    
    # This is the problematic case
    bad_indexed.loc[{'dim_0': 0}] = HasValues()
    print(f"bad_indexed.values: {bad_indexed.values}")
    print(f"Type of first element in bad_indexed: {type(bad_indexed.values[0])}")
    
    # The issue is that we expect bad_indexed.values[0] to be a HasValues instance,
    # but instead it gets coerced to array(5) because of the .values property
    expected_type = HasValues
    actual_type = type(bad_indexed.values[0])
    
    print(f"\nExpected type: {expected_type}")
    print(f"Actual type: {actual_type}")
    
    if actual_type != expected_type:
        print("❌ BUG REPRODUCED: The object was coerced instead of stored as-is!")
        return False
    else:
        print("✅ ISSUE FIXED: The object was stored as-is!")
        return True


if __name__ == "__main__":
    test_issue_reproduction()
import pytest
import mazeRunner


# Test Settings

def test_Settings_init_adds_attributes():
    pass

def test_Settings_init_error_nonLiteral_inputs():
    pass

# Test Runner

def test_Runner_init_rect_big_enough_to_contain_radius():
    pass

def test_Runner_init_acc_is_positive():
    pass

def test_Runner_set_direction_gives_unit_vector_or_zero():
    pass

def test_Runner_set_direction_zero_when_opposing_inputs_used():
    pass

def test_Runner_set_direction_zero_when_no_inputs_used():
    pass

def test_Runner_set_direction_maps_single_inputs_to_vector():
    pass

def test_Runner_set_direction_maps_diagonal_inputs_to_vector():
    pass

def test_Runner_move_updates_vel():
    pass

def test_Runner_move_calls_set_rect_pos():
    pass

def test_Runner_move_keeps_pos_is_mediator_approve_fails():
    pass

def test_Runner_move_changes_pos_is_mediator_approve_pass():
    pass

def test_Runner_set_rec_pos_rounds_rect_to_ints():
    pass

def test_Runner_set_rec_centers_circle_at_pos():
    pass

# Test Square (formerly Block)

def test_Square_init_set_vars_to_inputs():
    #pos
    #color
    #size
    pass

# Test Circle (formerly Objective)

def test_Circle_init_set_vars_to_inputs():
    #pos
    #color
    #size (radius)
    pass

# Test SpriteMediator

def test_Mediator_init_creates_all_sprites():
    pass

def test_Mediator_init_store_sprite_appends_if_group_exists():
    pass

def test_Mediator_init_store_sprite_adds_new_if_group_new():
    pass

def test_Mediator_regiser_inputs_saves_cmds():
    pass

def test_Mediator_update_moves_runner():
    pass

def test_Mediator_approve_move_call_circle_collide_rect():
    pass

def test_Mediator_update_checks_victory_condition():
    pass

# Test View

# Test MazeRunner

# Test Geometry

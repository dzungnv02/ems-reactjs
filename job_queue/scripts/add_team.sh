#!/bin/bash
wpId=$1
team_name="$2"
team_path=$3
echo $wpId
echo $team_name
echo $team_path
cd ~/local-wp/wpadmintools/apitools/
./add_new_team.sh $wpId "$team_name" $team_path


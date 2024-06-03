from flask import request, jsonify
from datetime import datetime
from .models import db, Team, TeamResult

import logging
logging.basicConfig(level=logging.DEBUG)

def configure_routes(app):
    @app.route('/')
    def hello():
        return 'Hello, World!'


    @app.route('/teams', methods=['POST'])
    def create_team():
        logging.debug("Received request to create team.")
        data = request.get_json()
        try:
            if not all(key in data for key in ['name', 'results']):
                return jsonify({"error": "Missing data"}), 400
            if not all(key in data['results'] for key in ['passing', 'failing', 'pending']):
                return jsonify({"error": "Incomplete results data"}), 400

            team = Team.query.filter_by(name=data['name']).first()
            if team:
                return jsonify({"error": "Team already exists"}), 400

            new_team = Team(
                name=data['name'],
                passing=data['results']['passing'],
                failing=data['results']['failing'],
                pending=data['results']['pending']
            )
            db.session.add(new_team)
            db.session.commit()
            return jsonify({"message": "Team created successfully"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500

    # @app.route('/teams', methods=['POST'])
    # def create_team():
    #     data = request.get_json()
    #
    #     # Validate that all required fields are present
    #     required_top_level_fields = ['name', 'results']
    #     required_result_fields = ['passing', 'failing', 'pending']
    #
    #     # Check for top-level fields
    #     if not all(field in data for field in required_top_level_fields):
    #         return jsonify({"error": "Missing required data"}), 400
    #
    #     # Check for nested results fields
    #     if not all(field in data['results'] for field in required_result_fields):
    #         return jsonify({"error": "Incomplete results data"}), 400
    #
    #     new_team = Team(
    #         name=data['name'],
    #         passing=data['results']['passing'],
    #         failing=data['results']['failing'],
    #         pending=data['results']['pending']
    #     )
    #     db.session.add(new_team)
    #     db.session.commit()
    #     return jsonify({"message": "Team created successfully"}), 201

    @app.route('/teams/summary', methods=['GET'])
    def get_team_summaries():
        teams = db.session.query(Team).add_columns(Team.name, Team.passing, Team.failing, Team.pending).all()
        teams_data = [
            {
                'name': team.Team.name,  # Access model instance attributes
                'totals': {
                    'passing': team.Team.passing,
                    'failing': team.Team.failing,
                    'pending': team.Team.pending
                }
            } for team in teams
        ]

        result = db.session.query(
            db.func.sum(Team.passing).label('total_passing'),
            db.func.sum(Team.failing).label('total_failing'),
            db.func.sum(Team.pending).label('total_pending')
        ).one()

        summary = {
            'passing': result.total_passing or 0,
            'failing': result.total_failing or 0,
            'pending': result.total_pending or 0
        }

        response = {
            'summary': summary,
            'teams': teams_data
        }

        return jsonify(response)

    @app.route('/teams/<team_name>', methods=['GET'])
    def get_team(team_name):
        team = Team.query.filter_by(name=team_name).first()
        if not team:
            return jsonify({'message': 'Team not found'}), 404

        result = {
            'name': team.name,
            'latest_results': {
                'passing': team.passing,
                'failing': team.failing,
                'pending': team.pending
            },
            'last_updated': team.last_updated.isoformat()  # ISO 8601 format
        }
        return jsonify(result), 200

    @app.route('/teams/<team_name>/all', methods=['GET'])
    def get_all_team_results(team_name):
        team = Team.query.filter_by(name=team_name).first()
        if not team:
            return jsonify({'message': 'Team not found'}), 404

        results_history = [{
            'date': result.created_at.isoformat(),
            'passing': result.passing,
            'failing': result.failing,
            'pending': result.pending
        } for result in team.results]

        response = {
            'name': team.name,
            'latest_results': results_history[-1] if results_history else {},
            'last_updated': team.last_updated.isoformat() if team.last_updated else None,
            'history': results_history
        }
        return jsonify(response), 200

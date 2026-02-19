const app = {
    currentView: 'dashboard',
    tournaments: [],

    init() {
        console.log('App v1.1.0 initializing...');
        try {
            this.bindEvents();
            this.loadView(this.currentView);
        } catch (error) {
            console.error('App failed to initialize:', error);
        }
    },

    bindEvents() {
        console.log('Binding events...');
        document.querySelectorAll('.sidebar-nav li').forEach(li => {
            li.addEventListener('click', (e) => {
                const view = e.currentTarget.dataset.view;
                console.log('Switching to view:', view);
                this.loadView(view);

                // Update active state
                document.querySelectorAll('.sidebar-nav li').forEach(el => el.classList.remove('active'));
                e.currentTarget.classList.add('active');
            });
        });

        const btnLogin = document.getElementById('btn-login');
        if (btnLogin) {
            btnLogin.addEventListener('click', () => {
                console.log('Login clicked');
                this.showLogin();
            });
        }

        const closeModal = document.querySelector('.close-modal');
        if (closeModal) {
            closeModal.addEventListener('click', () => {
                document.getElementById('modal-container').classList.add('hidden');
            });
        }
    },

    async loadView(view) {
        console.log('Loading view:', view);
        this.currentView = view;
        const contentArea = document.getElementById('content-area');
        const viewTitle = document.getElementById('view-title');

        if (!contentArea || !viewTitle) {
            console.error('Core UI elements not found!');
            return;
        }

        this.showLoader(true);

        try {
            switch (view) {
                case 'dashboard':
                case 'tournaments': {
                    viewTitle.innerText = view === 'dashboard' ? 'Dashboard Overview' : 'All Tournaments';
                    const tournaments = await API.getTournaments();
                    console.log('Fetched tournaments:', tournaments);
                    contentArea.innerHTML = Components.TournamentList(tournaments);
                    break;
                }
                case 'results': {
                    viewTitle.innerText = 'Global Recent Results';
                    const matches = await API.getRecentMatches();
                    contentArea.innerHTML = Components.RecentResultsView(matches);
                    break;
                }
                case 'rankings': {
                    viewTitle.innerText = 'Global Player Rankings';
                    const rankings = await API.getRankings();
                    contentArea.innerHTML = Components.RankingsView(rankings);
                    break;
                }
            }
        } catch (error) {
            console.error('Error loading view:', error);
            contentArea.innerHTML = `<div class="error-state">Error loading data: ${error.message}</div>`;
        } finally {
            this.showLoader(false);
        }
    },

    async showTournament(id) {
        console.log('Showing tournament:', id);
        this.showLoader(true);
        const viewTitle = document.getElementById('view-title');
        const contentArea = document.getElementById('content-area');

        try {
            const tournament = await API.getTournament(id);
            const standings = await API.getStandings(id);
            console.log('Standings loaded:', standings);

            viewTitle.innerText = tournament.name;
            contentArea.innerHTML = Components.TournamentDashboard(tournament, standings);
        } catch (error) {
            console.error('Error showing tournament:', error);
            contentArea.innerHTML = `<div class="error-state">Error showing tournament: ${error.message}</div>`;
        } finally {
            this.showLoader(false);
        }
    },

    async showAddTeam(tournamentId) {
        console.log('Showing Add Team modal for:', tournamentId);
        const modal = document.getElementById('modal-container');
        const modalTitle = document.getElementById('modal-title');
        const modalContent = document.getElementById('modal-content');

        if (!modal || !modalTitle || !modalContent) {
            console.error('Modal elements not found!');
            return;
        }

        this.showLoader(true);
        try {
            const tournament = await API.getTournament(tournamentId);
            modalTitle.innerText = `Add Team to ${tournament.name}`;
            modalContent.innerHTML = Components.AddTeamForm(tournamentId, tournament.is_doubles);
            modal.classList.remove('hidden');

            const form = document.getElementById('add-team-form');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const rawData = Object.fromEntries(formData.entries());

                    const data = {
                        name: rawData.name,
                        tournament_id: parseInt(rawData.tournament_id),
                        players: []
                    };

                    if (rawData.player1) data.players.push(rawData.player1);
                    if (rawData.player2) data.players.push(rawData.player2);

                    console.log('Submitting new team...', data);
                    try {
                        await API.createTeam(data);
                        modal.classList.add('hidden');
                        alert('Team added successfully!');
                        this.showTournament(tournamentId);
                    } catch (error) {
                        console.error('Error adding team:', error);
                        alert('Error adding team: ' + error.message);
                    }
                });
            }
        } catch (error) {
            console.error('Error showing add team flow:', error);
            alert('Error loading tournament details: ' + error.message);
        } finally {
            this.showLoader(false);
        }
    },

    async generateFixtures(id) {
        if (!confirm('This will generate new fixtures. Continue?')) return;
        console.log('Generating fixtures for:', id);
        this.showLoader(true);
        try {
            await API.generateFixtures(id);
            alert('Fixtures generated successfully!');
            this.showTournament(id);
        } catch (error) {
            console.error('Error generating fixtures:', error);
            alert('Error: ' + error.message);
        } finally {
            this.showLoader(false);
        }
    },

    showCreateTournament() {
        console.log('Showing Create Tournament modal');
        const modal = document.getElementById('modal-container');
        const modalTitle = document.getElementById('modal-title');
        const modalContent = document.getElementById('modal-content');

        modalTitle.innerText = 'Create New Tournament';
        modalContent.innerHTML = Components.CreateTournamentForm();
        modal.classList.remove('hidden');

        const form = document.getElementById('create-tournament-form');
        if (form) {
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                console.log('Creating tournament...');
                const formData = new FormData(e.target);
                const data = Object.fromEntries(formData.entries());
                data.num_participants = parseInt(data.num_participants);
                data.points_per_win = parseInt(data.points_per_win) || 2;
                data.points_per_draw = parseInt(data.points_per_draw) || 1;
                data.is_doubles = data.is_doubles === 'true';

                try {
                    await API.createTournament(data);
                    modal.classList.add('hidden');
                    this.loadView('tournaments');
                } catch (error) {
                    console.error('Error creating tournament:', error);
                    alert('Error: ' + error.message);
                }
            });
        }
    },

    async deleteTournament(id) {
        if (!confirm('Are you sure you want to delete this tournament? This will remove all teams and match history.')) return;

        console.log('Deleting tournament:', id);
        this.showLoader(true);
        try {
            await API.deleteTournament(id);
            alert('Tournament deleted successfully!');
            this.loadView('tournaments');
        } catch (error) {
            console.error('Error deleting tournament:', error);
            alert('Error: ' + error.message);
        } finally {
            this.showLoader(false);
        }
    },

    async showScoring(matchId) {
        console.log('Showing Scoring modal for match:', matchId);
        const modal = document.getElementById('modal-container');
        const modalTitle = document.getElementById('modal-title');
        const modalContent = document.getElementById('modal-content');

        this.showLoader(true);
        try {
            // Find match in current tournament data or fetch it
            const tournaments = await API.getTournaments();
            let targetMatch = null;
            let targetTournament = null;

            for (const t of tournaments) {
                const fullT = await API.getTournament(t.id);
                targetMatch = fullT.matches.find(m => m.id === matchId);
                if (targetMatch) {
                    targetTournament = fullT;
                    break;
                }
            }

            if (!targetMatch) throw new Error('Match not found');

            modalTitle.innerText = `Update Score: ${targetMatch.team1.name} vs ${targetMatch.team2.name}`;
            modalContent.innerHTML = Components.ScoringForm(targetMatch, targetTournament);
            modal.classList.remove('hidden');

            const form = document.getElementById('scoring-form');
            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault();
                    const formData = new FormData(e.target);
                    const rawData = Object.fromEntries(formData.entries());

                    const scores = [
                        {
                            team_id: targetMatch.team1_id,
                            runs: parseInt(rawData.score1) || 0,
                            sets_won: parseInt(rawData.score1) || 0,
                            wickets: parseInt(rawData.wickets1) || 0
                        },
                        {
                            team_id: targetMatch.team2_id,
                            runs: parseInt(rawData.score2) || 0,
                            sets_won: parseInt(rawData.score2) || 0,
                            wickets: parseInt(rawData.wickets2) || 0
                        }
                    ];

                    try {
                        await API.updateScore(matchId, scores);
                        modal.classList.add('hidden');
                        alert('Score updated successfully!');
                        this.showTournament(targetTournament.id);
                    } catch (error) {
                        console.error('Error updating score:', error);
                        alert('Error: ' + error.message);
                    }
                });
            }
        } catch (error) {
            console.error('Error opening scoring modal:', error);
            alert('Error: ' + error.message);
        } finally {
            this.showLoader(false);
        }
    },

    showLoader(show) {
        const loader = document.getElementById('loader');
        if (loader) loader.classList.toggle('hidden', !show);
    },

    showLogin() {
        alert('Admin login feature coming soon! Default credentials: admin / password123');
    }
};

// Expose to window
window.app = app;
window.API = API;
window.Components = Components;

document.addEventListener('DOMContentLoaded', () => {
    app.init();
});

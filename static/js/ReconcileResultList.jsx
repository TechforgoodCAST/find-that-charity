import React from "react";
import ReconcileResultMatched from "./ReconcileResultMatched"
import ReconcileResult from "./ReconcileResult"
import AutoComplete from "./AutoComplete"

export default class ReconcileResultList extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            confirmed: null,
            matched: (props.matches[0].match ? props.matches[0] : null),
            matches: props.matches,
            show_matches: 3,
            show_suggest: false,
            show_preview: false
        };
        this.selectInput = this.selectInput.bind(this);
        this.unmatch = this.unmatch.bind(this);
        this.showMore = this.showMore.bind(this);
        this.showFewer = this.showFewer.bind(this);
        this.showSuggest = this.showSuggest.bind(this);
        this.hideSuggest = this.hideSuggest.bind(this);
    }

    match_url(){
        return `/adddata/${this.props.file_id}/match`;
    }

    selectInput(result) {
        this.setState({ matched: result })
        var formData = new FormData();
        formData.append("row", this.props.row);
        formData.append("match_id", result.id);

        fetch(this.match_url(), {body: formData, method: 'POST'})
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            console.log(myJson);
        });
    }

    unmatch(result) {
        this.setState({ matched: null });
        var formData = new FormData();
        formData.append("row", this.props.row);
        formData.append("match_id", "");

        fetch(this.match_url(), {body: formData, method: 'POST'})
        .then(function (response) {
            return response.json();
        })
        .then(function (myJson) {
            console.log(myJson);
        });
    }

    showMore(e) {
        e.preventDefault();
        this.setState({ show_matches: Math.min(this.state.matches.length, this.state.show_matches + 3) })
    }

    showFewer(e) {
        e.preventDefault();
        this.setState({ show_matches: Math.max(this.state.show_matches - 3, 3) })
    }

    showSuggest(e) {
        e.preventDefault();
        this.setState({ show_suggest: true })
    }

    hideSuggest(e) {
        e.preventDefault();
        this.setState({ show_suggest: false })
    }

    render() {
        if (this.state.matched) {
            return <ReconcileResultMatched result={this.state.matched} unmatch={this.unmatch} />;
        }
        return (
            <div>
                {this.state.matches.map((match, i) =>
                    i < this.state.show_matches &&
                    <ReconcileResult key={i} result={match} selectInput={this.selectInput} />
                )}
                <span className="is-size-7">
                    <span className="has-text-grey">{this.state.show_matches + " of " + this.state.matches.length + " results"}</span>
                    {' '}
                    {this.state.matches.length > this.state.show_matches &&
                        <a href="#" onClick={this.showMore}>[more]</a>}
                    {' '}
                    {this.state.show_matches > 3 &&
                        <a href="#" onClick={this.showFewer}>[fewer]</a>}
                    {' '}
                    {this.state.show_suggest &&
                        <a href="#" onClick={this.hideSuggest}>[hide search]</a>}
                    {' '}
                    {!this.state.show_suggest &&
                        <a href="#" onClick={this.showSuggest}>[show search]</a>}
                </span>
                {this.state.show_suggest &&
                    <div>
                        <AutoComplete selectInput={this.selectInput} />
                    </div>}
            </div>
        );
    }
}
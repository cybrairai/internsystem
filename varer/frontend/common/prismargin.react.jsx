/** @jsx React.DOM */
angular.module('cyb.varer').factory('PrisMargin', function ($filter) {
    return React.createClass({
        propTypes: {
            requiredInnpris: React.PropTypes.number,
            requiredUtpris: React.PropTypes.number,
            requiredUtMva: React.PropTypes.number
        },
        render: function () {
            var eksmva = this.props.utPris / (1 + this.props.utMva/100);
            var margin = (((eksmva - this.props.innPris) / eksmva) * 100);
            var theClass;

            if (margin > 150)
                theClass = 'prismargin-veryhigh';
            else if (margin > 100)
                theClass = 'prismargin-higher';
            else if (margin > 50)
                theClass = 'prismargin-high';
            else if (margin > 20)
                theClass = 'prismargin-ok';
            else if (margin > 10)
                theClass = 'prismargin-low';
            else if (margin < 0)
                theClass = 'prismargin-subzero';
            else
                theClass = 'prismargin-verylow';

            var difftext;
            if (margin < 0) {
                difftext = 'Tap: ' + (eksmva - this.props.innPris);
            } else {
                difftext = 'Fortjeneste: ' + (eksmva - this.props.innPris);
            }

            margin = margin.toFixed(1).toString().replace('.', ',');

            return (
                <span className={'prismargin ' + theClass} title={difftext}>{margin} %
                    <span className="prismargin-kr"> ({$filter('price')(eksmva - this.props.innPris, 2)})</span>
                </span>);
        }
    });
});

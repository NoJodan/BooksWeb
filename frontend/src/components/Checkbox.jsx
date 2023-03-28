

export const Checkbox = ({onChange = (e) => {}, label = ""}) => {
    
    return (
        <div className="form-check" style={{textAlign: 'left'}}>
            <input className="form-check-input" onChange={e => onChange(e)} type="checkbox" id="flexCheckDefault" />
            {
                label !== "" ? (<label className="form-check-label" htmlFor="flexCheckDefault">{label}</label>) : undefined
            }
        </div>
    )
}
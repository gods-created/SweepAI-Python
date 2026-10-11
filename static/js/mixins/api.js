let EVALUATE_ACTION_CONTROLLER = null;

export const evaluateAction = async (code1, code2) => {
    if (EVALUATE_ACTION_CONTROLLER !== null) {
        EVALUATE_ACTION_CONTROLLER.abort();
        EVALUATE_ACTION_CONTROLLER = null;
    }

    EVALUATE_ACTION_CONTROLLER = new AbortController();

    try {
        const request = await fetch('/api/agent/evaluate', {
            method: 'POST',
            signal: EVALUATE_ACTION_CONTROLLER.signal,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code1: code1,
                code2: code2
            })
        });

        const response = await request.json();

        if (!request.ok) {
            return {
                status: false,
                err_description:
                    response.err_description ??
                    `Request failed with status ${request.status}`
            };
        }

        return response;
    } catch (e) {
        if (e.name === 'AbortError') {
            return {};
        }

        return {
            status: false,
            err_description: e.message ?? 'Something went wrong'
        };
    }
};